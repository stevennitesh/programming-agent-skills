# Durable decisions

Read when a specification or domain update is useful. Capture decisions for a
future reader, not a transcript of every conversational turn.

## Choose and update the owner

Follow relevant repository guidance for specs, domain records, and ADRs when
present. An absent convention need not block a local draft: choose an existing
documentation location or state a proposed destination. Do not silently change
a configured publication or domain route. Keep a proposal local when writing the
intended authoritative destination is unavailable or outside authorization.

For domain meaning or an ADR, use [Domain modeling](domain-modeling.md) to select
the distinction, current owner, and useful record. The publication and dependent
write rules below apply to that path as well as specifications.

## Reconcile competing documents

Before publishing or revising a spec, inspect existing plans, specs, guides, and
agent-facing pointers about the same outcome. Follow relevant links and search
for competing instructions; keep this check bounded to the affected work.
Distinguish current authority, proposals, and historical evidence. Age alone does
not make a document obsolete, and a new proposal does not supersede accepted work.

Reconcile a useful document in place when only part needs changing. When an
accepted replacement makes a local document wholly obsolete, move it out of the
active context into repository-root `.archive/`, retaining its relative path or
another collision-free identity. Preserve still-governing portions and historical
decision evidence; apply the domain reference's supersession rules to ADRs.
Do not leave two documents presenting conflicting instructions as current.

Within the authorized document-update scope, make the replacement readable before
archiving its predecessor. Update affected indexes, agent pointers, and links to
the current owner; keep historical links explicitly historical and repair relative
links affected by the move. Verify destinations stay within the repository and
do not overwrite an archive entry. For externally hosted plans, use the configured
supersession mechanism within authority rather than implying a local archive
retires the external source. Report unresolved ownership or unapplied consequences.

## Preserve the contract

Use the project's vocabulary and identify the source of material commitments.
Read the relevant source in full, including decision-changing comments or linked
decisions. For conflicting or multi-owner inputs, a small source-to-decision map
can prevent lost commitments; it is not mandatory for a single clear conversation.

Describe the problem, outcome, boundaries, settled behavior, meaningful acceptance,
and open risks or deferrals. Include public/data contracts, trust, privacy, and
operational constraints when they affect this work. A small schema or prototype
fragment may express a settled rule better than prose; label its evidence limits.
Use stable code pointers where helpful, without freezing a speculative file list,
implementation sequence, or test ownership into the specification.

Re-read the result as a fresh implementer. Can they recover the same outcome and
recognize success without guessing a consequential decision? Keep proposed changes
distinct from accepted requirements. Updating a spec should reconcile affected
acceptance and references rather than append contradictory current truth.

## Revisions during delivery

Before changing accepted meaning already used by tickets or workers, identify the
affected source revision, commitments, ticket identities, assignments, and proof.
Coordinate with the execution owner before changing an active worker's contract;
do not edit its ticket, release its claim, or redefine success behind its back.
Return the exact changed commitments and affected work when execution control is
outside this task's authority. Keep a proposed revision distinct from the current
accepted source until its decision and coordinated application are settled.

For an authorized revision, the execution owner pauses affected dispatch and
quiesces affected writers before changing their assignments. Reconcile the accepted
source, dependent ticket acceptance, gates and worker instructions together; keep
affected pending work non-ready until that reconciliation is verified. Revalidate
landed behavior and invalidate proof only where the changed contract affects it.
Preserve unaffected work and history. Do not reuse a former completion verdict to
claim the revised outcome; identify further implementation or evidence required.
Resume affected work only against the reconciled accepted revision.

## Publish only within authority

A requested local spec may be written directly under applicable repository rules.
If the destination is a tracker or other external system, inspect the target and
verify the supported write and read-back operations first. Reuse an existing
matching artifact; do not overwrite divergent or ambiguously owned content.
When approval is needed, present the concrete proposed effect after preparation;
do not reopen authorization already supplied by the user.

For dependent domain or ADR updates, make replacement truth readable before
removing displaced material. Stop on a failed or uncertain write, inspect every
attempted target, and report the remaining consequences.

After an authorized write, read back the intended content and identity. If a
create has an uncertain result, inspect before retrying so it does not become a
duplicate. Report partial or unknown state accurately. Specification publication
does not imply tickets, readiness labels, implementation, or Git publication.
