# Audit and change records

Read for a multi-entry audit or before applying approved memory changes.

## Account for the selected set

Use stable entry identities or source locations. For each atomic claim record:

```text
Entry/claim | Kind | Authority/current owner | Disposition
Destination | Evidence or gap | Reason | Proposed statement (if changing)
```

Use keep, generalize, migrate, expire, or review. Account for every original
entry, including every claim split from a mixed entry. Give totals by disposition
for an audit; totals count claims, with the original entry count separately when
splitting changes the number. Do not hide unreadable or unexamined entries in
expiry totals. Mark audit coverage incomplete and name the missing evidence.

Compare apparent duplicates semantically: scope, trigger, exceptions, and intended
behavior must match. Retain distinct conditions rather than collapsing similar
wording. Contradictions require the current authority or an explicit unresolved
decision, not whichever statement is newest-looking or most frequently copied.

For migration, name the actual existing destination and the knowledge it must
preserve. If that owner does not yet contain the needed meaning, report migration
as proposed. Do not remove the only useful active copy merely because a destination
has been suggested. Verify both coverage and retrieval before calling it redundant.

## Apply a bounded authorized update

Prepare a concrete change set: store and entry identities, current text or hashes,
replacement/removal intent, preserved content, and exclusions. Avoid repeating
sensitive contents in the report. For destructive or materially partial effects,
establish a recovery method; do not promise an archive or version history without
checking it exists. Preserve historical evidence unless its exact deletion is
separately authorized.

Use existing user authority and the store/runtime's supported update mechanism.
Refresh targets immediately before the effect; relevant drift stops the affected
change for reconciliation. Do not overwrite another edit. On an unresolved failure
stop dependent mutations, inspect actual partial state, and avoid replaying an
indeterminate update. Do not broaden cleanup to make a retry easier.

Verify at the actual effect boundary: intended retained meanings present, removed
active meanings absent, unrelated context preserved. For duplicate summaries or
indexes in the selected store, check the surfaces that can still retrieve the
meaning; deleting one entry alone may not remove it from active context. Do not
delete historical sources just because they remain searchable as evidence.

Report one of: audit complete (no writes), audit incomplete (coverage gaps),
update pending (request recorded, effects unverified), or update applied (all
authorized effects verified). Partial failure stays pending with exact completed
and unresolved effects and next safe action. A successful file write is enough
only when that file itself is the authorized active-store boundary.
