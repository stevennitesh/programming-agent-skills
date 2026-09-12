# Audit and change records

Read for audits or before applying authorized context cleanup.

## Account for the selected set

For a repository-wide audit, discover candidate context beyond existing links:
agent instructions, documentation indexes, plans/specs, context records, ADRs,
and relevant guides. Include unlinked documents and search for obsolete paths,
commands, skill names, or workflow conventions. For a narrower audit, keep
discovery within the requested boundary and its affected routes.

Check candidates against current code, configuration, accepted decisions, and
delivery state. Distinguish incorrect current guidance, completed or superseded
plans still presented as active, historical evidence worth retaining, and
unverified material needing investigation. Age or a missing inbound link alone
does not establish obsolescence.

For repository audits, identify assessed surfaces and affected routes, findings or
no-change outcomes, current owners or proposed actions, verification, and coverage
gaps. Give exact proposed wording when changing meaning. Group equivalent outcomes;
a disposition for every sentence is unnecessary.

For memory entries, use stable identities and preserve distinct claims. Split
claims when authority, scope, or disposition differs. Keep, generalize, migrate,
expire, and review are useful dispositions; record destination, evidence or gap,
reason, and proposed wording when changing meaning. Totals are optional unless
the store requires them. Account for the selected set without treating unreadable
or unexamined entries as obsolete.

Compare apparent duplicates semantically: scope, trigger, exceptions, and intended
behavior must match. Retain distinct conditions rather than collapsing similar
wording. Contradictions require the current authority or an explicit unresolved
decision, not whichever statement is newest-looking or most frequently copied.

For migration, name the actual existing destination and the knowledge it must
preserve. If that owner does not yet contain the needed meaning, report migration
as proposed. Do not remove the only useful active copy merely because a destination
has been suggested. Verify both coverage and retrieval before calling it redundant.

## When domain meaning or decisions need a record

When the audit identifies useful project meaning or decision rationale without a
durable owner, or cleanup affects existing domain meaning, accepted decisions,
or ADR applicability, follow configured repository domain guidance and read
[Domain modeling](../../shape-work/references/domain-modeling.md). This supplies
record-selection and reconciliation guidance without starting shaping.

Prefer updating an existing owner. When none fits, suggest the smallest suitable
addition: a context document for durable meaning future work would otherwise
infer, or an ADR for a settled consequential tradeoff. Missing files alone do not
justify creating them, and a proposal does not authorize creation.

## Apply a bounded authorized update

Prepare a concrete change set: file or entry identities, replacement/removal
intent, preserved content, and exclusions. Capture hashes or snapshots when needed
for concurrency, recovery, or the storage mechanism. Avoid repeating
sensitive contents in the report. For destructive or materially partial effects,
establish a recovery method; do not promise an archive or version history without
checking it exists. Preserve historical evidence unless its exact deletion is
separately authorized.

For repository instruction edits, verify current ownership through affected
pointers and when superseded documents are opened directly, using the authoring
guidance selected by the main skill. Archiving alone does not retire competing
instructions.

When reconciling or retiring repository documents, follow
[Document reconciliation](../../shape-work/references/durable-decisions.md#reconcile-competing-documents).
It owns in-place reconciliation, archival of wholly superseded documents under
repository-root `.archive/`, preservation, and affected-pointer verification.

For memory changes, use the store/runtime's supported update mechanism.
Refresh targets immediately before the effect; relevant drift stops the affected
change for reconciliation. Do not overwrite another edit. On an unresolved failure
stop dependent mutations, inspect actual partial state, and avoid replaying an
indeterminate update. Do not broaden cleanup to make a retry easier.

Verify at the actual effect boundary: intended retained meanings present, removed
active meanings absent, unrelated context preserved. For duplicate summaries or
indexes in the selected store, check the surfaces that can still retrieve the
meaning; deleting one entry alone may not remove it from active context. Do not
delete historical sources just because they remain searchable as evidence.

Report verified changes and any pending or failed effects, with the remaining
check or next safe action. A successful write proves completion only when the
written file itself is the authorized active-context boundary.
