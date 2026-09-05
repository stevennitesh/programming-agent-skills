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
