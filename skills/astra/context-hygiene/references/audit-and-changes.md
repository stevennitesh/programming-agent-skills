# Audit and change records

Read for a persistent-context audit or before applying authorized cleanup.

## Discover the selected surface

For a repository-wide audit, discover relevant context beyond existing links:
agent instructions, context records, plans or specifications presented as current,
decision records, indexes, and guides. Include unlinked material and search for
obsolete paths, commands, skill names, or workflow conventions. For a narrower
audit, keep discovery within the requested boundary and its affected routes.

Check candidates against current code, configuration, accepted decisions, and
delivery state. Distinguish:

- incorrect or misleading current guidance;
- completed or superseded material still presented as active;
- historical evidence worth retaining; and
- unverified material that needs investigation rather than cleanup.

Age, repetition, or a missing inbound link alone does not establish obsolescence.

Compare apparent duplicates semantically. Scope, trigger, exceptions, authority,
and intended behavior must match before one copy can safely replace another.
Resolve contradictions through the current owner or leave the decision explicit;
do not choose whichever statement looks newest or appears most often.

When migrating knowledge to another owner, identify the actual destination and the
meaning it must preserve. Do not remove the only useful active copy merely because
a destination has been proposed. Verify that the replacement owner contains the
needed meaning and that future agents can retrieve it.

## Route changes to the right owner

Context hygiene decides whether information should remain durable and where it
belongs.

For agent-instruction wording, triggers, pointers, and reconciliation, use
[writing-for-agents](../../writing-for-agents/SKILL.md).

When useful project meaning or decision rationale lacks a durable owner, follow
the repository's domain guidance. Use
[Domain modeling](../../shape-work/references/domain-modeling.md) when deciding how
accepted meaning or consequential decision rationale should be represented. Do
not create a domain record merely because a preferred file is missing.

Repository setup or pack migration belongs to
[repo-bootstrap](../../repo-bootstrap/SKILL.md) when that outcome was requested;
an audit finding does not start it automatically.

## Apply a bounded authorized update

Before mutation, identify the exact files or entries to change and the meaning to
preserve, replace, or remove. Refresh mutable targets when drift could cause one
writer to overwrite another.

Preserve historical evidence unless deleting or rewriting it is part of the
authorized effect. Archiving a file does not by itself retire active instructions
that still reach future agents through another path.

For managed-memory changes, use the runtime's supported mechanism. After a partial
or uncertain effect, inspect actual state before retrying rather than replaying an
indeterminate mutation.

Verify at the real retrieval boundary:

- intended retained meanings are still available;
- stale active meanings no longer reach future agents within scope;
- replacement owners are reachable;
- unrelated context remains intact; and
- historical sources remain evidence rather than accidentally active authority.

Deleting one duplicate summary or index entry does not prove a meaning disappeared
from active context if another retrieval surface still exposes it.

Report verified changes, coverage gaps, and any pending or failed effects. A
successful write proves completion only when the written object itself is the
authorized active-context boundary.
