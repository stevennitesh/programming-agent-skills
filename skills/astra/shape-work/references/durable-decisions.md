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
accepted replacement makes a local document wholly obsolete, prefer removing the
superseded file and relying on verified Git history. Preserve still-governing
portions and decision evidence at their current owner first; preserve uncommitted
content before removal. Archive only when repository policy or a concrete retention
need warrants it. Apply the domain reference's supersession rules to ADRs.
Do not leave two documents presenting conflicting instructions as current.

Before relocating or retiring a document, check affected inbound links and code
or test consumers. Reconcile affected consumers within scope, or retain the
document in place with clear applicability when relocation cannot be completed
safely.

Within the authorized document-update scope, make the replacement readable before
retiring its predecessor. Update affected indexes, agent pointers, and links to
the current owner; keep historical links explicitly historical. If archiving,
repair moved relative links, verify destinations stay within the repository, and
do not overwrite an archive entry. For externally hosted plans, use the configured
supersession mechanism within authority rather than implying a local archive
retires the external source. Report unresolved ownership or unapplied consequences.

## Preserve the contract

Keep a short purpose statement at the existing spec or plan owner: the problem,
who benefits, the desired improvement, and why the scoped capability is sufficient.
Preserve consequential exclusions and their reasons. Distinguish user intent from
inferred rationale; do not invent a purpose to justify a proposed mechanism.
Pair it with concrete behaviors that distinguish success from consequential failure
and evidence for those behaviors, rather than an exhaustive behavior catalog.

Use the project's vocabulary and identify the source of material commitments.
Inspect the source sections and linked decisions needed to preserve material
commitments, including decision-changing comments. Read the full source when their
scope or context is unclear. For conflicting or multi-owner inputs, a small source-to-decision map
can prevent lost commitments; it is not mandatory for a single clear conversation.

Preserve public/data contracts, trust, privacy, and operational constraints when
they affect this work. A small schema or prototype
fragment may express a settled rule better than prose; label its evidence limits.
Use stable code pointers where helpful, without freezing a speculative file list,
implementation sequence, or test ownership into the specification.

Re-read the result as a fresh implementer. Can they recover why the work matters,
the intended outcome, and sufficient evidence without guessing a consequential
decision? Purpose guides implementation choices, not exceptions to accepted
requirements; surface conflicts with their owner. Keep proposed changes
distinct from accepted requirements. Updating a spec should reconcile affected
acceptance and references rather than append contradictory current truth.

## Plans for coordinated delivery

When coordinated implementation is requested, keep one authoritative plan with
two distinguishable parts. The accepted contract holds purpose, outcome, scope,
operating assumptions, consequential design decisions, and acceptance. The delivery approach
holds coherent slices, dependencies, justified checkpoint coverage, and concise
progress. Link existing owners instead of copying their contracts. Keep model
settings, worker-guidance paths and hashes, checkout state, custody, and repair
accounting in assignments, continuation handoffs, or the existing execution-state
owner.

Detail approaching work while resolving dependencies that could invalidate the
overall approach. Leave routine internal design to the implementer. Delivery order
can change within scope; accepted commitments change only through their decision
owner. Writing a mechanism into the approach does not make it binding acceptance.
The selected execution workflow owns checkpoint scheduling, custody, correction
allowances, and final review. This plan shape does not authorize execution or
require a separate plan document when an existing owner is sufficient.

## Completed milestone records

Completed milestone records retain project decisions, delivered behavior, evidence,
limitations, and relevant next steps. Retain execution details only when needed to explain provenance or unresolved
work. Preserve custody, authorization, and repair accounting while work remains
active or resumable; do not discard recovery state to tidy a document. Apply this
when completing or revising current records, not as a rewrite of historical evidence.

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
